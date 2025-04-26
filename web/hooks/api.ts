import React from "react";
import axios from "axios";
import { useQuery, useMutation } from "react-query";
import { qc } from "@/lib/qc";

export interface Action {
  id: string;
  name: string;
  description: string;
}

export interface Macro {
  id: string;
  name: string;
  prompt: string;
  allow_other_actions: boolean;
  required_actions: Action[];
}

export interface User {
  id: string;
}

export interface CreateMacroInput {
  name: string;
  prompt: string;
  allow_other_actions: boolean;
  required_actions: string[];
}

const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

/* ------------------------------- user hooks ------------------------------- */
export const useCreateUser = () => {
  return useMutation<User, Error, unknown>(() => api.post<User>("/users").then((res) => res.data), {
    onSuccess: (data) => {
      qc.setQueryData<User>("currentUser", data);
    },
  });
};

export const useLazyGetUser = () => {
  const [loading, setLoading] = React.useState(false);

  const getUser = async ({ id }: { id: string }) => {
    setLoading(true);
    try {
      const response = await api.get<User>(`/users/${id}`);
      return { data: response.data };
    } catch (error) {
      console.error("Failed to fetch user:", error);
      return { data: null };
    } finally {
      setLoading(false);
    }
  };

  return [getUser, { loading }] as const;
};

export const useDeleteUser = () => {
  return useMutation<void, Error, string>((userId) => api.delete(`/users/${userId}`).then(() => {}), {
    onSuccess: (_data, userId) => {
      qc.removeQueries(["userMacros", userId]);
      qc.removeQueries("currentUser");
    },
  });
};

export const useGetUser = (userId: string) => {
  return useQuery<User, Error>(
    ["currentUser", userId],
    () => api.get<User>(`/users/${userId}`).then((res) => res.data),
    {
      enabled: !!userId,
    }
  );
};

/* ------------------------------ action hooks ------------------------------ */
export const useActions = () => {
  return useQuery<Action[], Error>("actions", () => api.get<Action[]>("/actions").then((res) => res.data));
};

export const useCreateAction = () => {
  return useMutation<Action, Error, Omit<Action, "id">>(
    ({ name, description }) =>
      api
        .post<Action>(
          "/actions",
          { name, description },
          {
            headers: { "X-Admin-Key": process.env.REACT_APP_ADMIN_KEY || "" },
          }
        )
        .then((res) => res.data),
    {
      onSuccess: () => {
        qc.invalidateQueries("actions");
      },
    }
  );
};

export const useEditAction = () => {
  return useMutation<Action, Error, Action>(
    ({ id, name, description }) =>
      api
        .put<Action>(
          `/actions/${id}`,
          { name, description },
          {
            headers: { "X-Admin-Key": process.env.REACT_APP_ADMIN_KEY || "" },
          }
        )
        .then((res) => res.data),
    {
      onSuccess: () => {
        qc.invalidateQueries("actions");
      },
    }
  );
};

export const useDeleteAction = () => {
  return useMutation<void, Error, number>(
    (id) =>
      api
        .delete(`/actions/${id}`, {
          headers: { "X-Admin-Key": process.env.REACT_APP_ADMIN_KEY || "" },
        })
        .then(() => {}),
    {
      onSuccess: () => {
        qc.invalidateQueries("actions");
      },
    }
  );
};

/* ------------------------------- macro hooks ------------------------------ */
export const useUserMacros = (userId: string) => {
  return useQuery<Macro[], Error>(
    ["userMacros", userId],
    () => api.get<Macro[]>(`/users/${userId}/macros`).then((res) => res.data),
    {
      enabled: !!userId,
    }
  );
};

export const useCreateMacro = (userId: string) => {
  return useMutation<Macro, Error, CreateMacroInput>(
    (input) =>
      api
        .post<Macro>("/macros", input, {
          headers: { "X-User-ID": userId },
        })
        .then((res) => res.data),
    {
      onSuccess: () => {
        qc.invalidateQueries(["userMacros", userId]);
      },
    }
  );
};

export const useEditMacro = (userId: string) => {
  return useMutation<Macro, Error, Macro>(
    ({ id, name, prompt, allow_other_actions, required_actions }) =>
      api
        .put<Macro>(
          `/macros/${id}`,
          {
            name,
            prompt,
            allow_other_actions,
            required_actions,
          },
          {
            headers: { "X-User-ID": userId },
          }
        )
        .then((res) => res.data),
    {
      onSuccess: () => {
        qc.invalidateQueries(["userMacros", userId]);
      },
    }
  );
};

export const useDeleteMacro = () => {
  return useMutation<string, Error, { macro_id: string; user_id: string }>(
    ({ macro_id, user_id }) =>
      api
        .delete(`/macros/${macro_id}`, {
          headers: { "X-User-ID": user_id },
        })
        .then(() => {
          return user_id;
        }),
    {
      onSuccess: (userId) => {
        qc.invalidateQueries(["userMacros", userId]);
      },
    }
  );
};

/* ------------------------------ utility hooks ----------------------------- */
export const useUploadAudio = (userId: string) => {
  return useMutation<{ filename: string; path: string }, Error, File>((file) => {
    const formData = new FormData();
    formData.append("file", file);
    return api
      .post("/upload", formData, {
        headers: {
          "X-User-ID": userId,
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => res.data);
  });
};
