"use client";

import { useUser } from "@clerk/nextjs";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import { useEffect, useRef, useState, useCallback } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { formatMessageTime } from "@/lib/utils";
import { ArrowLeft, Send, Trash2 } from "lucide-react";

const REACTION_EMOJIS = ["👍", "❤️", "😂", "😮", "😢"];

interface ChatAreaProps {
  conversationId: Id<"conversations">;
  currentUserConvexId: Id<"users"> | null;
  onBack?: () => void;
}

export default function ChatArea({
  conversationId,
  currentUserConvexId,
  onBack,
}: ChatAreaProps) {
  const { user } = useUser();
  const [messageText, setMessageText] = useState("");
  const [isUserScrolledUp, setIsUserScrolledUp] = useState(false);
  const [showNewMessageBtn, setShowNewMessageBtn] = useState(false);
  const [showReactionMenuFor, setShowReactionMenuFor] = useState<string | null>(null);

  // ── Delete confirmation state ──
  const [messageToDelete, setMessageToDelete] = useState<Id<"messages"> | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // ── Send error/retry state ──
  const [sendError, setSendError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // ── Queries ──
  const messages = useQuery(api.messages.getMessages, { conversationId });

  const conversations = useQuery(
    api.conversations.getUserConversations,
    currentUserConvexId ? { userId: currentUserConvexId } : "skip"
  );
  const currentConversation = conversations?.find((c) => c._id === conversationId);

  const typingUsers = useQuery(
    api.presence.getTypingUsers,
    currentUserConvexId
      ? { conversationId, currentUserId: currentUserConvexId }
      : "skip"
  );

  // ── Mutations ──
  const sendMessage = useMutation(api.messages.sendMessage);
  const deleteMessage = useMutation(api.messages.deleteMessage);
  const toggleReaction = useMutation(api.messages.toggleReaction);
  const setTyping = useMutation(api.presence.setTyping);
  const markAsRead = useMutation(api.conversations.markAsRead);

  // ── Mark as read when opening or new messages arrive ──
  useEffect(() => {
    if (currentUserConvexId && messages && messages.length > 0) {
      markAsRead({ conversationId, userId: currentUserConvexId });
    }
  }, [conversationId, currentUserConvexId, messages?.length]);

  // ── Auto-scroll to bottom ──
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    setShowNewMessageBtn(false);
  }, []);

  // ── Detect if user scrolled up ──
  const handleScroll = () => {
    const container = scrollContainerRef.current;
    if (!container) return;
    const isAtBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 100;
    setIsUserScrolledUp(!isAtBottom);
    if (isAtBottom) setShowNewMessageBtn(false);
  };

  // ── When new messages arrive ──
  useEffect(() => {
    if (!messages) return;
    if (isUserScrolledUp) {
      setShowNewMessageBtn(true);
    } else {
      scrollToBottom();
    }
  }, [messages?.length]);

  // ── Typing indicator handler ──
  const handleTyping = (value: string) => {
    setMessageText(value);
    if (!currentUserConvexId) return;

    if (value.trim()) {
      setTyping({ conversationId, userId: currentUserConvexId, isTyping: true });
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      typingTimeoutRef.current = setTimeout(() => {
        setTyping({ conversationId, userId: currentUserConvexId, isTyping: false });
      }, 2000);
    } else {
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      setTyping({ conversationId, userId: currentUserConvexId, isTyping: false });
    }
  };

  // ── Send message ──
  const handleSendMessage = async () => {
    if (!messageText.trim() || !currentUserConvexId) return;

    const textToSend = messageText.trim();
    setSendError(null);

    // Clear typing indicator
    if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
    setTyping({ conversationId, userId: currentUserConvexId, isTyping: false });

    setMessageText("");
    setIsUserScrolledUp(false);

    try {
      await sendMessage({
        conversationId,
        senderId: currentUserConvexId,
        content: textToSend,
      });
      scrollToBottom();
    } catch (error) {
      // Restore message so user can retry
      setSendError("Failed to send. Tap retry to try again.");
      setMessageText(textToSend);
    }
  };

  // ── Confirm and execute delete ──
  const handleConfirmDelete = async () => {
    if (!messageToDelete) return;
    setIsDeleting(true);
    try {
      await deleteMessage({ messageId: messageToDelete });
    } finally {
      setIsDeleting(false);
      setMessageToDelete(null);
    }
  };

  // ── Cleanup typing on unmount / conversation change ──
  useEffect(() => {
    return () => {
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      if (currentUserConvexId) {
        setTyping({ conversationId, userId: currentUserConvexId, isTyping: false });
      }
    };
  }, [conversationId]);

  // ── Enter key to send ──
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const otherUser = currentConversation?.otherUsers[0];

  return (
    <div className="flex flex-col h-full bg-gray-50">

      {/* ── Chat Header ── */}
      <div className="bg-white border-b p-4 flex items-center gap-3 flex-shrink-0">
        {onBack && (
          <button
            onClick={onBack}
            className="md:hidden p-1 rounded hover:bg-slate-100"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
        )}
        <div className="relative">
          <Avatar className="h-10 w-10">
            <AvatarImage
              src={currentConversation?.isGroup ? undefined : otherUser?.imageUrl}
            />
            <AvatarFallback
              className={currentConversation?.isGroup ? "bg-purple-100 text-purple-600" : ""}
            >
              {currentConversation?.isGroup
                ? "👥"
                : otherUser?.name?.[0] ?? "?"}
            </AvatarFallback>
          </Avatar>
          {!currentConversation?.isGroup && otherUser?.isOnline && (
            <span className="absolute bottom-0 right-0 h-3 w-3 rounded-full bg-green-500 border-2 border-white" />
          )}
        </div>
        <div>
          <p className="font-semibold text-slate-800">
            {currentConversation?.isGroup
              ? currentConversation.groupName
              : otherUser?.name ?? "Loading..."}
          </p>
          <p className="text-xs text-slate-500">
            {currentConversation?.isGroup
              ? `👥 ${currentConversation.participantIds.length} members`
              : otherUser?.isOnline
              ? "🟢 Online"
              : "⚫ Offline"}
          </p>
        </div>
      </div>

      {/* ── Messages Area ── */}
      <div
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {messages === undefined ? (
          // Loading skeleton
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className={`flex ${i % 2 === 0 ? "justify-end" : ""} animate-pulse`}
              >
                <div
                  className={`h-10 rounded-2xl ${
                    i % 2 === 0 ? "bg-blue-200" : "bg-slate-200"
                  } w-48`}
                />
              </div>
            ))}
          </div>
        ) : messages.length === 0 ? (
          // Empty state
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="font-semibold text-slate-700 mb-1">No messages yet</h3>
            <p className="text-slate-400 text-sm">Be the first to say hello!</p>
          </div>
        ) : (
          // Message list
          messages.map((message) => {
            const isMyMessage = message.senderId === currentUserConvexId;

            return (
              <div
                key={message._id}
                className={`flex ${
                  isMyMessage ? "justify-end" : "justify-start"
                } group`}
              >
                {/* Other user avatar */}
                {!isMyMessage && (
                  <Avatar className="h-8 w-8 mr-2 mt-1 flex-shrink-0">
                    <AvatarImage src={message.sender?.imageUrl} />
                    <AvatarFallback>{message.sender?.name?.[0]}</AvatarFallback>
                  </Avatar>
                )}

                <div
                  className={`max-w-[70%] ${
                    isMyMessage ? "items-end" : "items-start"
                  } flex flex-col`}
                >
                  {/* Sender name for group or other user */}
                  {!isMyMessage && (
                    <p className="text-xs text-slate-500 mb-1 ml-1">
                      {message.sender?.name}
                    </p>
                  )}

                  {/* Message bubble */}
                  <div className="relative">
                    <div
                      className={`px-4 py-2 rounded-2xl text-sm ${
                        message.isDeleted
                          ? "bg-slate-100 text-slate-400 italic"
                          : isMyMessage
                          ? "bg-blue-500 text-white"
                          : "bg-white text-slate-800 shadow-sm"
                      }`}
                    >
                      {message.content}

                      {/* Delete button — opens confirmation modal */}
                      {isMyMessage && !message.isDeleted && (
                        <button
                          onClick={() => setMessageToDelete(message._id)}
                          className="absolute -left-8 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-red-50 rounded"
                          title="Delete message"
                        >
                          <Trash2 className="h-4 w-4 text-red-400" />
                        </button>
                      )}
                    </div>

                    {/* Reaction button */}
                    {!message.isDeleted && (
                      <button
                        onClick={() =>
                          setShowReactionMenuFor(
                            showReactionMenuFor === message._id
                              ? null
                              : message._id
                          )
                        }
                        className="absolute -bottom-2 right-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs bg-white border rounded-full px-1 shadow-sm hover:bg-slate-50"
                      >
                        😊
                      </button>
                    )}

                    {/* Reaction picker */}
                    {showReactionMenuFor === message._id && (
                      <div className="absolute bottom-6 right-0 bg-white border rounded-full shadow-lg flex gap-1 p-1 z-10">
                        {REACTION_EMOJIS.map((emoji) => (
                          <button
                            key={emoji}
                            onClick={() => {
                              if (currentUserConvexId) {
                                toggleReaction({
                                  messageId: message._id,
                                  userId: currentUserConvexId,
                                  emoji,
                                });
                              }
                              setShowReactionMenuFor(null);
                            }}
                            className="text-lg hover:scale-125 transition-transform"
                          >
                            {emoji}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Reactions display */}
                  {message.reactions && message.reactions.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                      {message.reactions.map((reaction) => (
                        <button
                          key={reaction.emoji}
                          onClick={() => {
                            if (currentUserConvexId) {
                              toggleReaction({
                                messageId: message._id,
                                userId: currentUserConvexId,
                                emoji: reaction.emoji,
                              });
                            }
                          }}
                          className={`text-xs rounded-full px-2 py-0.5 border flex items-center gap-0.5 transition-colors ${
                            currentUserConvexId &&
                            reaction.userIds.includes(currentUserConvexId)
                              ? "bg-blue-50 border-blue-200"
                              : "bg-white border-slate-200"
                          }`}
                        >
                          {reaction.emoji} {reaction.userIds.length}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Timestamp */}
                  <p
                    className={`text-xs text-slate-400 mt-1 ${
                      isMyMessage ? "text-right" : "text-left"
                    }`}
                  >
                    {formatMessageTime(message._creationTime)}
                  </p>
                </div>
              </div>
            );
          })
        )}

        {/* Typing indicator */}
        {typingUsers && typingUsers.length > 0 && (
          <div className="flex items-center gap-2">
            <Avatar className="h-6 w-6">
              <AvatarImage src={typingUsers[0]?.imageUrl} />
              <AvatarFallback>{typingUsers[0]?.name?.[0]}</AvatarFallback>
            </Avatar>
            <div className="bg-white rounded-2xl px-4 py-2 shadow-sm">
              <div className="flex gap-1 items-center h-4">
                <span className="text-xs text-slate-500 mr-1">
                  {typingUsers[0]?.name} is typing
                </span>
                <div
                  className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0ms" }}
                />
                <div
                  className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"
                  style={{ animationDelay: "150ms" }}
                />
                <div
                  className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"
                  style={{ animationDelay: "300ms" }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* ── ↓ New Messages floating button ── */}
      {showNewMessageBtn && (
        <div className="fixed bottom-24 left-1/2 -translate-x-1/2 z-20">
          <button
            onClick={scrollToBottom}
            className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-full shadow-lg transition-all animate-bounce"
          >
            ↓ New messages
          </button>
        </div>
      )}

      {/* ── Send Error Banner with Retry ── */}
      {sendError && (
        <div className="bg-red-50 border-t border-red-200 px-4 py-2 flex items-center justify-between flex-shrink-0">
          <p className="text-red-600 text-xs">{sendError}</p>
          <button
            onClick={() => {
              setSendError(null);
              handleSendMessage();
            }}
            className="text-xs text-red-600 font-semibold underline hover:text-red-800 ml-3"
          >
            Retry
          </button>
        </div>
      )}

      {/* ── Message Input ── */}
      <div className="bg-white border-t p-4 flex-shrink-0">
        <div className="flex gap-2">
          <Input
            placeholder="Type a message..."
            value={messageText}
            onChange={(e) => handleTyping(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 rounded-full"
          />
          <Button
            onClick={handleSendMessage}
            disabled={!messageText.trim()}
            size="icon"
            className="rounded-full bg-blue-500 hover:bg-blue-600"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* ── DELETE CONFIRMATION MODAL ── */}
      {messageToDelete && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 flex flex-col items-center text-center">

            {/* Red trash icon */}
            <div className="h-16 w-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <Trash2 className="h-8 w-8 text-red-500" />
            </div>

            {/* Title */}
            <h2 className="text-lg font-semibold text-slate-800 mb-2">
              Delete Message?
            </h2>

            {/* Description */}
            <p className="text-sm text-slate-500 mb-6 leading-relaxed">
              Are you sure you want to delete this message? Everyone will see{" "}
              <span className="italic font-medium text-slate-600">
                "This message was deleted"
              </span>
              . This action cannot be undone.
            </p>

            {/* Buttons */}
            <div className="flex gap-3 w-full">
              {/* Cancel */}
              <button
                onClick={() => setMessageToDelete(null)}
                disabled={isDeleting}
                className="flex-1 py-2.5 px-4 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors text-sm font-medium disabled:opacity-50"
              >
                Cancel
              </button>

              {/* Confirm Delete */}
              <button
                onClick={handleConfirmDelete}
                disabled={isDeleting}
                className="flex-1 py-2.5 px-4 bg-red-500 hover:bg-red-600 text-white rounded-xl transition-colors text-sm font-medium disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isDeleting ? (
                  <>
                    <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Deleting...
                  </>
                ) : (
                  "Yes, Delete"
                )}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
