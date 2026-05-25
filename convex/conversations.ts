import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Get or create a 1-on-1 conversation between two users
export const getOrCreateConversation = mutation({
  args: {
    currentUserId: v.id("users"),
    otherUserId: v.id("users"),
  },
  handler: async (ctx, args) => {
    // Look for an existing conversation with exactly these two people
    const allConversations = await ctx.db.query("conversations").collect();

    const existingConversation = allConversations.find((conv) => {
      const participants = conv.participantIds;
      return (
        !conv.isGroup &&
        participants.length === 2 &&
        participants.includes(args.currentUserId) &&
        participants.includes(args.otherUserId)
      );
    });

    if (existingConversation) {
      return existingConversation._id;
    }

    // Create new conversation
    const conversationId = await ctx.db.insert("conversations", {
      participantIds: [args.currentUserId, args.otherUserId],
      isGroup: false,
      lastMessageTime: Date.now(),
    });

    return conversationId;
  },
});

// Get all conversations for the current user (for the sidebar)
export const getUserConversations = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const allConversations = await ctx.db.query("conversations").collect();

    // Filter conversations where the current user is a participant
    const userConversations = allConversations.filter((conv) =>
      conv.participantIds.includes(args.userId)
    );

    // For each conversation, get the other user's info and last message
    const conversationsWithDetails = await Promise.all(
      userConversations.map(async (conv) => {
        // Get info about other participants
        const otherParticipantIds = conv.participantIds.filter(
          (id) => id !== args.userId
        );

        const otherUsers = await Promise.all(
          otherParticipantIds.map((id) => ctx.db.get(id))
        );

        // Get the last message
        const messages = await ctx.db
          .query("messages")
          .withIndex("by_conversation", (q) =>
            q.eq("conversationId", conv._id)
          )
          .collect();

        const lastMessage = messages[messages.length - 1];

        // Count unread messages
        const readReceipt = await ctx.db
          .query("readReceipts")
          .withIndex("by_conversation_user", (q) =>
            q.eq("conversationId", conv._id).eq("userId", args.userId)
          )
          .first();

        const unreadCount = readReceipt
          ? messages.filter(
              (m) =>
                m._creationTime > readReceipt.lastReadTime &&
                m.senderId !== args.userId
            ).length
          : messages.filter((m) => m.senderId !== args.userId).length;

        return {
          ...conv,
          otherUsers: otherUsers.filter(Boolean),
          lastMessage,
          unreadCount,
        };
      })
    );

    // Sort by most recent message
    return conversationsWithDetails.sort((a, b) => {
      const timeA = a.lastMessage?._creationTime ?? 0;
      const timeB = b.lastMessage?._creationTime ?? 0;
      return timeB - timeA;
    });
  },
});

// Create a group conversation
export const createGroupConversation = mutation({
  args: {
    participantIds: v.array(v.id("users")),
    groupName: v.string(),
  },
  handler: async (ctx, args) => {
    const conversationId = await ctx.db.insert("conversations", {
      participantIds: args.participantIds,
      isGroup: true,
      groupName: args.groupName,
      lastMessageTime: Date.now(),
    });
    return conversationId;
  },
});

// Mark conversation as read
export const markAsRead = mutation({
  args: {
    conversationId: v.id("conversations"),
    userId: v.id("users"),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("readReceipts")
      .withIndex("by_conversation_user", (q) =>
        q
          .eq("conversationId", args.conversationId)
          .eq("userId", args.userId)
      )
      .first();

    if (existing) {
      await ctx.db.patch(existing._id, { lastReadTime: Date.now() });
    } else {
      await ctx.db.insert("readReceipts", {
        conversationId: args.conversationId,
        userId: args.userId,
        lastReadTime: Date.now(),
      });
    }
  },
});
