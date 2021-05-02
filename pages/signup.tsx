import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSession, buildSession } from '../lib/client/session';
import { inputHandler, submitHandler } from '../lib/client/form';
import { authorizeGuest } from '../lib/client/authorization';
import Nav from '../lib/client/nav';
import { FormError } from '../lib/client/error';

export default function Signup(props){
    const router = useRouter();
    const auth = authorizeGuest(router);

    const [form, setForm] = useState({
        'first_name': 'Isaac',
        'last_name': 'Krementsov',
        'username': 'isaackrementsov',
        'password': 'isaackrementsov',
        'email': 'isaackrementsov@gmail.com',
        'instructor': false
    });
    const [res, setRes] = useState({});

    const handleInput = inputHandler(setForm);
    const handleSubmit = submitHandler('/api/user/', 'POST', form, setRes);

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
                    <h1>Sign Up</h1>
                    <hr/>
                    <FormError error={res.error}/>
                    <div className="flex-container-between">
                        <div className="label">
                            First Name
                            <input type="text" name="first_name" value={form.first_name} onChange={handleInput} required/>
                        </div>
                        <div className="label">
                            Last Name
                            <input type="text" name="last_name" value={form.last_name} onChange={handleInput} required/>
                        </div>
                    </div>
                    <div className="label">
                        Email
                        <input type="email" name="email" value={form.email} onChange={handleInput} required/>
                    </div>
                    <div className="flex-container-between">
                        <div className="label" style={{width: '55%'}}>
                            Username
                            <input type="text" name="username" value={form.username} onChange={handleInput} required/>
                        </div>
                        <div className="label checkbox-label" style={{minWidth: '35%', width: '35%'}}>
                            <div>
                                <input type="checkbox" name="instructor" checked={form.instructor} onChange={handleInput}/>
                                <span>I'm a teacher</span>
                            </div>
                        </div>
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
