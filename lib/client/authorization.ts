import { Authorization } from '../common-types';
import { useEffect } from 'react';

export const home = (userId: string) => {
    return '/user/' + userId;
}

export default function Authorize(authorization: Authorization, router) {
    return session => {
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

export const authorizeGuest = router => Authorize(Authorization.GUEST, router);
export const authorizeUser = router => Authorize(Authorization.USER, router);
export const authorizeInstructor = router => Authorize(Authorization.INSTRUCTOR, router);
