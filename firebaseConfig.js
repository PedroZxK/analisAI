// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDGuPUo5PjS4MyVTK4yQGRwlZ5FFllPsio",
  authDomain: "analisai-d3a91.firebaseapp.com",
  projectId: "analisai-d3a91",
  storageBucket: "analisai-d3a91.firebasestorage.app",
  messagingSenderId: "981537129539",
  appId: "1:981537129539:web:49640a2dc79faacb2380f6",
  measurementId: "G-P9PVFS2L5S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);