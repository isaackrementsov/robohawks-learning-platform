import { createStore } from 'redux';
import { sessionReducer, sessionService, loadUser, deleteUser } from 'redux-react-session';

const store = createStore(sessionReducer);
sessionService.initSessionService(store);

const KEYS = ['user_id', 'instructor', 'avatar'];

export const loggedIn = async () : Promise<Boolean> => {
    const session = await useSession();
    // Catch exception in case session is null/undefined
    try { return !!session['user_id']; }catch(_e){ return false; }
}

export const useValue = async (key: string) : Promise<any> => {
    const session = await useSession();
    return session[key];
}

export const useSession = async () : Promise<Object> => {
    return await loadUser();
}

export const buildSession = (data: Object) => {
    for(let key of KEYS){
        localStorage.setItem(key, data[key]);
    }

    localStorage.setItem('loggedIn', 'true');
}

export const destroySession = async () => {
    if(loggedIn()){
        localStorage.clear();
        await fetch('/user/auth', {method: 'DELETE'});
    }
}
