import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSession, buildSession } from '../lib/client/session';
import { inputHandler, submitHandler } from '../lib/client/form';
import { authorizeGuest } from '../lib/client/authorization';
import Nav from '../lib/client/nav';
import { FormError } from '../lib/client/error';

export default function Login(props){
    const router = useRouter();
    const auth = authorizeGuest(router);

    const [form, setForm] = useState({'identifier': '', 'password': ''});
    const [res, setRes] = useState({});

    const handleInput = inputHandler(setForm);
    const handleSubmit = submitHandler('/api/user/auth', 'POST', form, setRes);

    useEffect(useSession(session => {
        auth(session);

        if(res.user){
            buildSession(res.user);
            router.push('/user/' + res.user.id);
        }
    }), [res]);

    return (
        <div className="App gradient-app">
            <Nav logo={'logo-white'}/>
            <div className="jumbotron jumbotron-fluid gradient flex-container-center">
                <form onSubmit={handleSubmit}>
                    <h1>Log In</h1>
                    <hr/>
                    <FormError error={res.error}/>
                    <div className="label">
                        Username or email
                        <input type="text" name="identifier" value={form.identifier} onChange={handleInput} required/>
                    </div>
                    <div className="label">
                        Password
                        <input type="password" name="password" value={form.password} onChange={handleInput} required/>
                    </div>
                    <input type="submit" value="Submit"/>
                </form>
            </div>
        </div>
    );
}
