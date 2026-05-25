"use client";

import { useUser } from "@clerk/nextjs";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useEffect } from "react";

export default function UserSync() {
  const { user, isSignedIn } = useUser();
  const upsertUser = useMutation(api.users.upsertUser);
  const setOnlineStatus = useMutation(api.users.setOnlineStatus);

  useEffect(() => {
    if (isSignedIn && user) {
      // Save/update user profile in Convex
      upsertUser({
        clerkId: user.id,
        name: user.fullName ?? user.username ?? "Unknown",
        email: user.emailAddresses[0]?.emailAddress ?? "",
        imageUrl: user.imageUrl,
      });
    }
  }, [isSignedIn, user]);

  useEffect(() => {
    if (!isSignedIn || !user) return;

    // Set user as online when they visit
    setOnlineStatus({ clerkId: user.id, isOnline: true });

    // Set user as offline when they leave
    const handleBeforeUnload = () => {
      setOnlineStatus({ clerkId: user.id, isOnline: false });
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      setOnlineStatus({ clerkId: user.id, isOnline: false });
    };
  }, [isSignedIn, user]);

  return null; // This component renders nothing visually
}
