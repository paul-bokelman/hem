"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { type User, useCreateUser, useLazyGetUser } from "@/hooks/api";

interface UserContextValue {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { mutate: createUser } = useCreateUser();
  const [getUser] = useLazyGetUser();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUserId = localStorage.getItem("userId");

    if (storedUserId) {
      // fetch user lazy
      getUser({ id: storedUserId }).then((response) => {
        if (response?.data) {
          setUser(response.data);
        } else {
          // user doesn't exist -> create new user
          createNewUser();
        }
      });
    } else {
      // no user id found -> create new user
      createNewUser();
    }
  }, []);

  const createNewUser = () => {
    createUser(
      {},
      {
        onSuccess: (newUser) => {
          localStorage.setItem("userId", newUser.id);
          setUser(newUser);
        },
        onError: (error) => {
          console.error("Failed to create user:", error);
        },
      }
    );
  };

  return <UserContext.Provider value={{ user, setUser }}>{children}</UserContext.Provider>;
};

export const useUser = (): UserContextValue => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
