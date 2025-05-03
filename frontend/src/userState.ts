import {create} from 'zustand';

interface UserState {
    userID: number | null;
    email: string | null;
    setUserID: (userID: number | null) => void;
    setEmail: (email: string | null) => void;
    getUserID: () => number | null;
    getEmail: () => string | null;
}

export const useUserStore = create<UserState>((set, get) => ({
    userID: null,
    email: null,
    setUserID: (userID) => set({ userID }),
    setEmail: (email) => set({ email }),
    getUserID: () => get().userID,
    getEmail: () => get().email,
}));
