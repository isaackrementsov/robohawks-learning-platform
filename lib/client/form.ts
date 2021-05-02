export function inputHandler(setForm){
    return e => {
        let val = e.target.value;
        let name = e.target.name;

        setForm(prevForm => {
            if(e.target.type === 'checkbox') val = !prevForm[name];

            return {
                ...prevForm,
                [name]: val
            }
        });
    }
}

export function submitHandler(uri: string, method: string, form, handleRes) : Function {
    return async e => {
        e.preventDefault();

        const res = await fetch(uri, {
            method: method,
            body: JSON.stringify(form),
            headers: {'Content-Type': 'application/json'}
        });
        const body = await res.json();

        handleRes(body);
    }
}
