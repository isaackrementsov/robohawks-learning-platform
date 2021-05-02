import { useSession } from './session';
import bodyParser from 'body-parser';

const globalMiddleware : Function[] = [
    useSession,
    bodyParser.json()
];
export default globalMiddleware;
