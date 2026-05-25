"use client";

import { useUser } from "@clerk/nextjs";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { UserButton } from "@clerk/nextjs";
import { formatMessageTime } from "@/lib/utils";
import { Id } from "@/convex/_generated/dataModel";
import { MessageSquare, Search, Users, UsersRound } from "lucide-react";

interface SidebarProps {
  selectedConversationId: Id<"conversations"> | null;
  onSelectConversation: (id: Id<"conversations">) => void;
  currentUserConvexId: Id<"users"> | null;
}

export default function Sidebar({
  selectedConversationId,
  onSelectConversation,
  currentUserConvexId,
}: SidebarProps) {
  const { user } = useUser();
  const [searchQuery, setSearchQuery] = useState("");
  const [showUserList, setShowUserList] = useState(false);

  // Group chat states
  const [showGroupModal, setShowGroupModal] = useState(false);
  const [selectedGroupMembers, setSelectedGroupMembers] = useState<Id<"users">[]>([]);
  const [groupName, setGroupName] = useState("");
  const [isCreatingGroup, setIsCreatingGroup] = useState(false);

  // Get all conversations for the sidebar
  const conversations = useQuery(
    api.conversations.getUserConversations,
    currentUserConvexId ? { userId: currentUserConvexId } : "skip"
  );

  // Get all other users for the user list
  const allUsers = useQuery(
    api.users.getAllUsers,
    user ? { currentClerkId: user.id } : "skip"
  );

  const getOrCreateConversation = useMutation(
    api.conversations.getOrCreateConversation
  );

  const createGroupConversation = useMutation(
    api.conversations.createGroupConversation
  );

  // Start a new conversation with a user
  const handleUserClick = async (otherUserId: Id<"users">) => {
    if (!currentUserConvexId) return;
    const conversationId = await getOrCreateConversation({
      currentUserId: currentUserConvexId,
      otherUserId,
    });
    onSelectConversation(conversationId);
    setShowUserList(false);
    setSearchQuery("");
  };

  // Toggle member selection for group chat
  const toggleGroupMember = (userId: Id<"users">) => {
    setSelectedGroupMembers((prev) =>
      prev.includes(userId)
        ? prev.filter((id) => id !== userId)
        : [...prev, userId]
    );
  };

  // Create group conversation
  const handleCreateGroup = async () => {
    if (!currentUserConvexId) return;
    if (groupName.trim() === "") return;
    if (selectedGroupMembers.length < 2) return;

    setIsCreatingGroup(true);
    try {
      // Include current user in the group
      const allMembers = [...selectedGroupMembers, currentUserConvexId];
      const conversationId = await createGroupConversation({
        participantIds: allMembers,
        groupName: groupName.trim(),
      });
      onSelectConversation(conversationId);
      // Reset everything
      setShowGroupModal(false);
      setSelectedGroupMembers([]);
      setGroupName("");
    } finally {
      setIsCreatingGroup(false);
    }
  };

  // Close group modal and reset
  const handleCloseGroupModal = () => {
    setShowGroupModal(false);
    setSelectedGroupMembers([]);
    setGroupName("");
  };

  // Filter users by search query
  const filteredUsers = allUsers?.filter((u) =>
    u.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Filter conversations by search query
  const filteredConversations = conversations?.filter((conv) => {
    const otherUser = conv.otherUsers[0];
    const name = conv.isGroup ? conv.groupName ?? "" : otherUser?.name ?? "";
    return name.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className="w-full md:w-80 bg-white border-r flex flex-col h-full">

      {/* Header */}
      <div className="p-4 border-b flex items-center justify-between bg-slate-50">
        <h1 className="text-xl font-bold text-slate-800">Messages</h1>
        <div className="flex items-center gap-2">

          {/* Create Group Button */}
          <button
            onClick={() => setShowGroupModal(true)}
            className="p-2 rounded-lg hover:bg-slate-200 transition-colors"
            title="Create group chat"
          >
            <UsersRound className="h-5 w-5 text-slate-600" />
          </button>

          {/* Toggle Users List Button */}
          <button
            onClick={() => {
              setShowUserList(!showUserList);
              setSearchQuery("");
            }}
            className={`p-2 rounded-lg transition-colors ${
              showUserList ? "bg-blue-100 text-blue-600" : "hover:bg-slate-200 text-slate-600"
            }`}
            title="Find users"
          >
            <Users className="h-5 w-5" />
          </button>

          <UserButton afterSignOutUrl="/sign-in" />
        </div>
      </div>

      {/* Search Bar */}
      <div className="p-3 border-b">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <Input
            placeholder={showUserList ? "Search users..." : "Search conversations..."}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {showUserList ? (

          // ── USER LIST VIEW ──
          <div>
            <div className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wide">
              All Users
            </div>
            {filteredUsers?.length === 0 ? (
              <div className="flex flex-col items-center justify-center p-8 text-center">
                <Users className="h-12 w-12 text-slate-300 mb-3" />
                <p className="text-slate-500 text-sm">No users found</p>
              </div>
            ) : (
              filteredUsers?.map((u) => (
                <button
                  key={u._id}
                  onClick={() => handleUserClick(u._id)}
                  className="w-full flex items-center gap-3 p-3 hover:bg-slate-50 transition-colors"
                >
                  <div className="relative">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={u.imageUrl} />
                      <AvatarFallback>{u.name[0]}</AvatarFallback>
                    </Avatar>
                    <span
                      className={`absolute bottom-0 right-0 h-3 w-3 rounded-full border-2 border-white ${
                        u.isOnline ? "bg-green-500" : "bg-gray-300"
                      }`}
                    />
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-sm text-slate-800">{u.name}</p>
                    <p className="text-xs text-slate-500">
                      {u.isOnline ? "🟢 Online" : "⚫ Offline"}
                    </p>
                  </div>
                </button>
              ))
            )}
          </div>

        ) : (

          // ── CONVERSATIONS LIST VIEW ──
          <div>
            {conversations === undefined ? (
              // Loading skeleton
              <div className="p-4 space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="flex items-center gap-3 animate-pulse">
                    <div className="h-12 w-12 bg-slate-200 rounded-full" />
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-slate-200 rounded w-3/4" />
                      <div className="h-3 bg-slate-200 rounded w-1/2" />
                    </div>
                  </div>
                ))}
              </div>
            ) : filteredConversations?.length === 0 ? (
              // Empty state
              <div className="flex flex-col items-center justify-center p-8 text-center mt-8">
                <MessageSquare className="h-16 w-16 text-slate-200 mb-4" />
                <h3 className="font-semibold text-slate-700 mb-1">
                  {searchQuery ? "No results found" : "No conversations yet"}
                </h3>
                <p className="text-slate-400 text-sm">
                  {searchQuery
                    ? "Try a different search term"
                    : "Click the Users icon to start chatting!"}
                </p>
              </div>
            ) : (
              // Conversation list
              filteredConversations?.map((conv) => {
                const otherUser = conv.otherUsers[0];
                const isSelected = conv._id === selectedConversationId;

                return (
                  <button
                    key={conv._id}
                    onClick={() => onSelectConversation(conv._id)}
                    className={`w-full flex items-center gap-3 p-3 transition-colors ${
                      isSelected ? "bg-blue-50 border-r-2 border-blue-500" : "hover:bg-slate-50"
                    }`}
                  >
                    {/* Avatar */}
                    <div className="relative flex-shrink-0">
                      <Avatar className="h-12 w-12">
                        <AvatarImage src={conv.isGroup ? undefined : otherUser?.imageUrl} />
                        <AvatarFallback
                          className={conv.isGroup ? "bg-purple-100 text-purple-600 text-lg" : ""}
                        >
                          {conv.isGroup ? "👥" : otherUser?.name?.[0] ?? "?"}
                        </AvatarFallback>
                      </Avatar>
                      {/* Online dot — only for 1-on-1 */}
                      {!conv.isGroup && otherUser?.isOnline && (
                        <span className="absolute bottom-0 right-0 h-3 w-3 rounded-full bg-green-500 border-2 border-white" />
                      )}
                    </div>

                    {/* Text info */}
                    <div className="flex-1 min-w-0 text-left">
                      <div className="flex justify-between items-center">
                        <p className="font-semibold text-sm text-slate-800 truncate">
                          {conv.isGroup ? conv.groupName : otherUser?.name}
                        </p>
                        {conv.lastMessage && (
                          <span className="text-xs text-slate-400 flex-shrink-0 ml-1">
                            {formatMessageTime(conv.lastMessage._creationTime)}
                          </span>
                        )}
                      </div>
                      <div className="flex justify-between items-center">
                        <p className="text-xs text-slate-500 truncate">
                          {conv.isGroup
                            ? `👥 ${conv.participantIds.length} members · ${
                                conv.lastMessage?.isDeleted
                                  ? "Message deleted"
                                  : conv.lastMessage?.content ?? "Start chatting"
                              }`
                            : conv.lastMessage?.isDeleted
                            ? "This message was deleted"
                            : conv.lastMessage?.content ?? "Start a conversation"}
                        </p>
                        {/* Unread badge */}
                        {conv.unreadCount > 0 && (
                          <Badge className="ml-1 h-5 w-5 flex items-center justify-center p-0 text-xs bg-blue-500 flex-shrink-0">
                            {conv.unreadCount > 9 ? "9+" : conv.unreadCount}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </button>
                );
              })
            )}
          </div>
        )}
      </div>

      {/* ── GROUP CREATION MODAL ── */}
      {showGroupModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md max-h-[85vh] flex flex-col">

            {/* Modal Header */}
            <div className="p-5 border-b flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-800">
                  Create Group Chat
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Select at least 2 members to continue
                </p>
              </div>
              <button
                onClick={handleCloseGroupModal}
                className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500 hover:text-slate-700"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-5 flex flex-col gap-4 flex-1 overflow-hidden">

              {/* Group Name Input */}
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1.5 block">
                  Group Name <span className="text-red-400">*</span>
                </label>
                <Input
                  placeholder="e.g. Team Alpha, Study Group, Family..."
                  value={groupName}
                  onChange={(e) => setGroupName(e.target.value)}
                  className="w-full"
                />
              </div>

              {/* Member Selection */}
              <div className="flex flex-col flex-1 overflow-hidden">
                <label className="text-sm font-medium text-slate-700 mb-2 block">
                  Add Members <span className="text-red-400">*</span>
                  <span className="text-slate-400 font-normal ml-1">
                    ({selectedGroupMembers.length} selected)
                  </span>
                </label>

                {/* Selected member chips */}
                {selectedGroupMembers.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-3">
                    {selectedGroupMembers.map((memberId) => {
                      const member = allUsers?.find((u) => u._id === memberId);
                      return (
                        <div
                          key={memberId}
                          className="flex items-center gap-1 bg-blue-100 text-blue-700 rounded-full px-3 py-1 text-sm"
                        >
                          <span>{member?.name}</span>
                          <button
                            onClick={() => toggleGroupMember(memberId)}
                            className="hover:text-blue-900 ml-1 font-bold leading-none"
                          >
                            ×
                          </button>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* User list */}
                <div className="overflow-y-auto flex-1 border rounded-xl divide-y divide-slate-100">
                  {allUsers?.length === 0 ? (
                    <div className="p-6 text-center text-slate-400 text-sm">
                      No other users found
                    </div>
                  ) : (
                    allUsers?.map((u) => {
                      const isSelected = selectedGroupMembers.includes(u._id);
                      return (
                        <button
                          key={u._id}
                          onClick={() => toggleGroupMember(u._id)}
                          className={`w-full flex items-center gap-3 p-3 transition-colors hover:bg-slate-50 ${
                            isSelected ? "bg-blue-50" : ""
                          }`}
                        >
                          {/* Checkbox circle */}
                          <div
                            className={`h-5 w-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all ${
                              isSelected
                                ? "bg-blue-500 border-blue-500"
                                : "border-slate-300"
                            }`}
                          >
                            {isSelected && (
                              <span className="text-white text-xs font-bold">✓</span>
                            )}
                          </div>

                          {/* Avatar */}
                          <div className="relative">
                            <Avatar className="h-9 w-9">
                              <AvatarImage src={u.imageUrl} />
                              <AvatarFallback>{u.name[0]}</AvatarFallback>
                            </Avatar>
                            {u.isOnline && (
                              <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-green-500 border-2 border-white" />
                            )}
                          </div>

                          {/* Name & status */}
                          <div className="text-left">
                            <p className="font-medium text-sm text-slate-800">
                              {u.name}
                            </p>
                            <p className="text-xs text-slate-400">
                              {u.isOnline ? "🟢 Online" : "⚫ Offline"}
                            </p>
                          </div>
                        </button>
                      );
                    })
                  )}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="p-5 border-t flex gap-3">
              <button
                onClick={handleCloseGroupModal}
                className="flex-1 py-2.5 px-4 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors text-sm font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateGroup}
                disabled={
                  isCreatingGroup ||
                  groupName.trim() === "" ||
                  selectedGroupMembers.length < 2
                }
                className="flex-1 py-2.5 px-4 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isCreatingGroup ? (
                  <>
                    <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    👥 Create Group
                    {selectedGroupMembers.length >= 2 && (
                      <span className="bg-blue-400 rounded-full px-1.5 py-0.5 text-xs">
                        {selectedGroupMembers.length + 1}
                      </span>
                    )}
                  </>
                )}
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
