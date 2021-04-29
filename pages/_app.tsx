import { AppProps } from 'next/app';
import '../public/css/App.css';
import '../public/css/Nav.css';
import '../public/css/Gradient.css';

export default function App({Component, pageProps}: AppProps){
    return <Component {...pageProps}/>
}
