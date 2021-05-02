import { home } from './authorization';
import { destroySession, useSession, useValue } from './session';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { CgAdd } from 'react-icons/cg';

export default function Nav(props){
    const [user, setUser] = useState({});
    const [logout, setLogout] = useState(false);
    const userHome = home(user['user_id']);
    const router = useRouter();


    useEffect(useSession(session => {
        setUser(session);

        if(logout){
            destroySession();
            router.push('/login');
        }
    }), [logout]);

    if(user['user_id']){
        return (
            <nav className="nav flex-column">
                <a className="navbar-brand h1" href={userHome}>
                    <div className="logo-small">
                        <img src="/img/logo.png" alt="logo"/>
                        <br/><p>LearnCVU</p>
                    </div>
                </a>
                { user['instructor'] ?
                    <>
                        <NavLink className="cta" href="/course/new"><CgAdd/><span>Create Course</span></NavLink>
                        <NavLink href="/course/all"><span>Find Courses</span></NavLink>
                    </>
                    :
                    <NavLink className="cta" href="/course/all"><CgAdd/><span>Find Courses</span></NavLink>
                }
                <NavLink href={userHome}><span>Dashboard</span></NavLink>
                <NavLink onClick={() => setLogout(true)} style={{cursor: 'pointer'}}><span>Logout</span></NavLink>
            </nav>
        )
    }else{
        return (
            <nav className="navbar navbar-expand-lg navbar-light horiz">
                <a className="navbar-brand h1 mb-0" href="/">
                    <img className="logo d-inline block align top" src={'/img/' + (props.logo || 'logo') + '.png'} alt="Logo"/>
                    <span id="title">LearnCVU</span>
                </a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
                    <ul className="navbar-nav">
                        <NavLink href="/login">Login</NavLink>
                        <NavLink className="cta" href="/signup">Signup</NavLink>
                    </ul>
                </div>
            </nav>
        )
    }
}

function NavLink(props){
    const [active, setActive] = useState(false);

    useEffect(function onFirstMount(){
        setActive(window.location.pathname === props.href);
    }, [setActive]);

    return (
        <li className="nav-item">
            <a
                href={props.href}
                className={(props.className || '') + ' nav-link' + (active ? ' active' : '')}
                onClick={props.onClick}
                style={props.style}
            >
                {props.children}
            </a>
        </li>
    );
}

export function PageHeader(props){
    const [avatar, setAvatar] = useState('');
    useEffect(useValue('avatar', data => setAvatar(data)), [setAvatar]);

    return (
        <nav className="navbar navbar-expand-lg navbar-light horiz part-nav" style={props.style}>
            <div className="navbar-brand h1 mb-0">
                <span>{props.title}</span>
            </div>
            <div className="navbar-collapse justify-content-end" id="navbarSupportedContent" style={{flexBasis: 0, flexGrow: 0}}>
                <ul className="navbar-nav">
                    {props.customNav ||
                        <li className="nav-item">
                            <a className="nav-link avatar" href="/account">
                                <div className="av-circle" style={{background: `url(/public/img/avatars/${avatar})`}}/>
                            </a>
                        </li>
                    }
                </ul>
            </div>
        </nav>
    );
}

export function PageLayout(props){
    return (
        <div className="App App-flex">
            <Nav/>
            <div className="content">
                <PageHeader title={props.title} style={props.style} customNav={props.customNav}/>
                <div className="col">
                    {props.children}
                </div>
            </div>
        </div>
    );
}
