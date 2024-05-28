import { type Firestore, getFirestore } from "firebase/firestore";
import { initializeApp, type FirebaseApp } from "firebase/app";

export let app: FirebaseApp;
export let db: Firestore;

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBXgaY1CB8g9FMmfs21tDYsj7vdk2W2X-g",
    authDomain: "trenddit-5f2a1.firebaseapp.com",
    projectId: "trenddit-5f2a1",
    storageBucket: "trenddit-5f2a1.appspot.com",
    messagingSenderId: "20098191655",
    appId: "1:20098191655:web:90b12b819c3eec12df9902"
};

export function initializeFirebase() {
    // Initialize Firebase
    app = initializeApp(firebaseConfig);
    db = getFirestore(app);
}