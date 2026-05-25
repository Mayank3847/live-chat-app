import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const setTyping = mutation({
  args: {
    conversationId: v.id("conversations"),
    userId: v.id("users"),
    isTyping: v.boolean(), // ADD THIS — true=typing, false=stopped
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("typingIndicators")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId)
      )
      .filter((q) => q.eq(q.field("userId"), args.userId))
      .first();

    if (!args.isTyping) {
      // User stopped typing — DELETE the record
      if (existing) {
        await ctx.db.delete(existing._id);
      }
      return;
    }

    // User is typing — upsert the record
    if (existing) {
      await ctx.db.patch(existing._id, { lastTyped: Date.now() });
    } else {
      await ctx.db.insert("typingIndicators", {
        conversationId: args.conversationId,
        userId: args.userId,
        lastTyped: Date.now(),
      });
    }
  },
});

export const getTypingUsers = query({
  args: {
    conversationId: v.id("conversations"),
    currentUserId: v.id("users"),
  },
  handler: async (ctx, args) => {
    const twoSecondsAgo = Date.now() - 2000;

    const typingIndicators = await ctx.db
      .query("typingIndicators")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId)
      )
      .collect();

    const activeTypers = typingIndicators.filter(
      (t) =>
        t.lastTyped > twoSecondsAgo &&
        t.userId !== args.currentUserId
    );

    const typingUsers = await Promise.all(
      activeTypers.map((t) => ctx.db.get(t.userId))
    );

    return typingUsers.filter(Boolean);
  },
});