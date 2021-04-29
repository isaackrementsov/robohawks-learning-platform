import { useSession, useValue } from './session';
import { useRouter } from 'next/router';
import { Authorization } from '../controller';

export const home = (userId?: string) => {
    const id = userId || useValue('user_id');
    return '/user/' + id;
}

export default function Authorize(authorization: Authorization) {
    return () => {
        const session = useSession();
        const router = useRouter();

        const userId = session['user_id'];
        const instructor = session['instructor'];
        const hasUserId = Boolean(userId);
        const userHome = home(userId);

        switch(authorization){
            case Authorization.GUEST:
                if(hasUserId) router.push(userHome);
                break;

            case Authorization.USER:
                if(!hasUserId) router.push('/login');
                break;

            case Authorization.INSTRUCTOR:
                if(!hasUserId) router.push('/login');
                else if(!instructor) router.push(userHome);
                break;

            default:
                break;
        }
    }
}

export const authorizeGuest = Authorize(Authorization.GUEST);
export const authorizeUser = Authorize(Authorization.USER);
export const authorizeInstructor = Authorize(Authorization.INSTRUCTOR);
