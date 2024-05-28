import { initializeFirebase } from '$lib/firebase';

/** @type {import('./$types').PageLoad} */
export function load() {
    initializeFirebase();
}