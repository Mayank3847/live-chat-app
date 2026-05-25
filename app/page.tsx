"use client";

import { useUser } from "@clerk/nextjs";
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import ChatArea from "@/components/ChatArea";
import UserSync from "@/components/UserSync";
import { Id } from "@/convex/_generated/dataModel";
import { MessageSquare } from "lucide-react";

export default function Home() {
  const { user } = useUser();
  const [selectedConversationId, setSelectedConversationId] =
    useState<Id<"conversations"> | null>(null);
  const [showMobileChat, setShowMobileChat] = useState(false);

  const currentConvexUser = useQuery(
    api.users.getUserByClerkId,
    user ? { clerkId: user.id } : "skip"
  );

  const handleSelectConversation = (id: Id<"conversations">) => {
    setSelectedConversationId(id);
    setShowMobileChat(true);
  };

  const handleBack = () => {
    setShowMobileChat(false);
  };

  return (
    <>
      <UserSync />
      {/* Full screen container */}
      <div className="h-screen w-screen flex overflow-hidden">
        
        {/* SIDEBAR — fixed width, hidden on mobile when chat open */}
        <div
          className={`
            ${showMobileChat ? "hidden" : "flex"}
            md:flex
            flex-col
            w-full md:w-80
            flex-shrink-0
            border-r border-gray-200
            bg-white
            overflow-hidden
          `}
        >
          <Sidebar
            selectedConversationId={selectedConversationId}
            onSelectConversation={handleSelectConversation}
            currentUserConvexId={currentConvexUser?._id ?? null}
          />
        </div>

        {/* CHAT AREA — takes ALL remaining space */}
        <div
          className={`
            ${showMobileChat ? "flex" : "hidden"}
            md:flex
            flex-col
            flex-1
            min-w-0
            overflow-hidden
            bg-gray-50
          `}
        >
          {selectedConversationId ? (
            <ChatArea
              conversationId={selectedConversationId}
              currentUserConvexId={currentConvexUser?._id ?? null}
              onBack={handleBack}
            />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8 h-full">
              <div className="bg-white rounded-full p-6 shadow-sm mb-4">
                <MessageSquare className="h-16 w-16 text-slate-300" />
              </div>
              <h2 className="text-xl font-semibold text-slate-700 mb-2">
                Welcome to Tars Chat
              </h2>
              <p className="text-slate-400 max-w-sm">
                Select a conversation from the sidebar or click the users icon to start chatting!
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}