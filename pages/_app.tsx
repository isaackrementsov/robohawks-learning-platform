import { AppProps } from 'next/app';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/Gradient.css';
import '../styles/App.css';
import '../styles/Nav.css';

export default function App({Component, pageProps}: AppProps){
    return <Component {...pageProps}/>
}
