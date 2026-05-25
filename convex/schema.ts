import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Users table - stores user profiles
  users: defineTable({
    clerkId: v.string(),        // Clerk's user ID
    name: v.string(),           // Display name
    email: v.string(),          // Email address
    imageUrl: v.string(),       // Profile picture URL
    isOnline: v.boolean(),      // Online/offline status
    lastSeen: v.number(),       // Timestamp of last activity
  })
    .index("by_clerk_id", ["clerkId"])   // Fast lookup by Clerk ID
    .index("by_email", ["email"]),        // Fast lookup by email

  // Conversations table - one-on-one or group chats
  conversations: defineTable({
    participantIds: v.array(v.id("users")),  // Array of user IDs in this chat
    isGroup: v.boolean(),                     // Is this a group chat?
    groupName: v.optional(v.string()),        // Group name (if group)
    lastMessageTime: v.optional(v.number()),  // For sorting conversations
    lastMessagePreview: v.optional(v.string()), // Preview text in sidebar
  }),

  // Messages table - individual messages
  messages: defineTable({
    conversationId: v.id("conversations"),  // Which conversation
    senderId: v.id("users"),                // Who sent it
    content: v.string(),                    // Message text
    isDeleted: v.boolean(),                 // Soft delete flag
    reactions: v.optional(
      v.array(
        v.object({
          emoji: v.string(),        // The emoji
          userIds: v.array(v.id("users")), // Who reacted
        })
      )
    ),
  })
    .index("by_conversation", ["conversationId"]), // Get all messages in a conversation

  // Typing indicators table
  typingIndicators: defineTable({
    conversationId: v.id("conversations"),
    userId: v.id("users"),
    lastTyped: v.number(),  // Timestamp — remove after 2 seconds
  })
    .index("by_conversation", ["conversationId"]),

  // Read receipts - tracks last read message per user per conversation
  readReceipts: defineTable({
    conversationId: v.id("conversations"),
    userId: v.id("users"),
    lastReadTime: v.number(),  // Timestamp of last read message
  })
    .index("by_conversation_user", ["conversationId", "userId"]),
});