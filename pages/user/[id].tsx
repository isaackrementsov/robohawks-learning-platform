import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { authorizeUser } from '../../lib/client/authorization';
import { useSession } from '../../lib/client/session';
import { PageLayout } from '../../lib/client/nav';
import { FormError } from '../../lib/client/error';

export default function Profile(props){
    const router = useRouter();
    const { id } = router.query;
    const auth = authorizeUser(router);

    const [error, setError] = useState(null);
    const [user, setUser] = useState({});
    const [currentUserId, setCurrentUserId] = useState(null);

    useEffect(useSession(async session => {
        auth(session);
        setCurrentUserId(session.user_id);

        const res = await fetch('/api/user/' + id);
        console.log(id, router.query);
        if(res.user){
            setUser(res.user);
            setError(null);
        }else if(res.error){
            setError(res.error);
        }
    }));

    return (
        <PageLayout title={user.id == currentUserId ? 'Dashboard' : user.username}>
            <FormError error={error}/>
            <h2>Credentials</h2>
            <h2>Courses</h2>
        </PageLayout>
    );

}
