const KEYS = ['user_id', 'instructor', 'avatar'];

export const useValue = (key: string, cb: Function) : Function => {
    if(KEYS.indexOf(key) == -1){
        cb(null);
    }else{
        return useSession(session => cb(session[key]));
    }
}

export const useSession = (cb: Function) : Function => {
    return () => {
        let session = {};

        for(let key of KEYS){
            let value = window.localStorage.getItem(key);

            try {
                session[key] = JSON.parse(value);
            }catch(_e){
                session[key] = value;
            }
        }

        cb(session);
    };
}

export const buildSession = (data: Object) : void => {
    for(let key of KEYS){
        window.localStorage.setItem(key, data[key]);
    }
}

export const destroySession = useSession(session => {
    if(session['user_id']){
        window.localStorage.clear();
        fetch('/user/auth', {method: 'DELETE'});
    }
});
