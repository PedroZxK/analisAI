import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyDGuPUo5PjS4MyVTK4yQGRwlZ5FFllPsio",
  authDomain: "analisai-d3a91.firebaseapp.com",
  projectId: "analisai-d3a91",
  storageBucket: "analisai-d3a91.firebasestorage.app",
  messagingSenderId: "981537129539",
  appId: "1:981537129539:web:49640a2dc79faacb2380f6",
  measurementId: "G-P9PVFS2L5S"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);