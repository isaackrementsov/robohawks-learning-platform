import { useSession } from './session';

const globalMiddleware : Function[] = [
    useSession
];
export default globalMiddleware;
