import {create} from 'zustand';

interface UserState {
    userID: number | null;
    email: string | null;
    givePrefrences: boolean;
    setGivePrefrences: (givePrefrences: boolean) => void;
    getGivePrefrences: () => boolean;
    setUserID: (userID: number | null) => void;
    setEmail: (email: string | null) => void;
    getUserID: () => number | null;
    getEmail: () => string | null;
}
export const useUserStore = create<UserState>((set, get) => ({
    userID: null,
    email: null,
    givePrefrences: true,
    setUserID: (userID) => set({ userID }),
    setEmail: (email) => set({ email }),
    setGivePrefrences: (givePrefrences) => set({ givePrefrences }),
    getUserID: () => get().userID,
    getEmail: () => get().email,
    getGivePrefrences: () => get().givePrefrences,
}));
