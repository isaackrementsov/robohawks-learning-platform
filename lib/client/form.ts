export function inputHandler(stateHook){
    let state, setState = stateHook;

    return e => {
        let val = e.target.value;
        let name = e.target.name;
        let updated = state['form'];

        if(e.target.type === 'checkbox'){
            updated[name] = !updated[name];
        }else{
            updated[name] = val;
        }

        setState({'form': updated});
    }
}

export function submitHandler(uri: string, method: string, stateHook) : Function {
    let state, setState = stateHook;

    return async e => {
        e.preventDefault();
        const form = state['form'];

        const res = await fetch(uri, {method: method, body: form});
        const body = await res.json();

        setState({'res': body});
    }
}
