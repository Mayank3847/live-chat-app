import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Get all messages in a conversation
export const getMessages = query({
  args: { conversationId: v.id("conversations") },
  handler: async (ctx, args) => {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId)
      )
      .collect();

    // For each message, get the sender's info
    const messagesWithSender = await Promise.all(
      messages.map(async (message) => {
        const sender = await ctx.db.get(message.senderId);
        return { ...message, sender };
      })
    );

    return messagesWithSender;
  },
});

// Send a new message
export const sendMessage = mutation({
  args: {
    conversationId: v.id("conversations"),
    senderId: v.id("users"),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    // Insert the message
    const messageId = await ctx.db.insert("messages", {
      conversationId: args.conversationId,
      senderId: args.senderId,
      content: args.content,
      isDeleted: false,
      reactions: [],
    });

    // Update the conversation's last message info
    await ctx.db.patch(args.conversationId, {
      lastMessageTime: Date.now(),
      lastMessagePreview: args.content,
    });

    return messageId;
  },
});

// Soft delete a message (doesn't remove from database)
export const deleteMessage = mutation({
  args: { messageId: v.id("messages") },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.messageId, {
      isDeleted: true,
      content: "This message was deleted",
    });
  },
});

// Add or remove a reaction to a message
export const toggleReaction = mutation({
  args: {
    messageId: v.id("messages"),
    userId: v.id("users"),
    emoji: v.string(),
  },
  handler: async (ctx, args) => {
    const message = await ctx.db.get(args.messageId);
    if (!message) return;

    const reactions = message.reactions ?? [];
    const existingReaction = reactions.find((r) => r.emoji === args.emoji);

    if (existingReaction) {
      // Toggle: if user already reacted, remove them; else add them
      if (existingReaction.userIds.includes(args.userId)) {
        // Remove user's reaction
        const updatedReactions = reactions
          .map((r) =>
            r.emoji === args.emoji
              ? { ...r, userIds: r.userIds.filter((id) => id !== args.userId) }
              : r
          )
          .filter((r) => r.userIds.length > 0); // Remove reaction if no users
        await ctx.db.patch(args.messageId, { reactions: updatedReactions });
      } else {
        // Add user to existing reaction
        const updatedReactions = reactions.map((r) =>
          r.emoji === args.emoji
            ? { ...r, userIds: [...r.userIds, args.userId] }
            : r
        );
        await ctx.db.patch(args.messageId, { reactions: updatedReactions });
      }
    } else {
      // Create new reaction
      await ctx.db.patch(args.messageId, {
        reactions: [...reactions, { emoji: args.emoji, userIds: [args.userId] }],
      });
    }
  },
});
