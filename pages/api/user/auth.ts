import { Authorization } from '../../../lib/common-types';
import RESTController from '../../../lib/controller';
import { newSession } from '../../../lib/session';
import client from '../../../lib/db';

export default RESTController(Authorization.NONE, {
    post: async (req, res) => {
        const identifier = req.body.identifier
        const password = req.body.password;

        const users = await client.user.findMany({
            where: {
                OR: [
                    {'email': identifier},
                    {'username': identifier}
                ],
                AND: [
                    {'password': password}
                ]
            }
        });
        const user = users[0];

        if(user){
            Object.assign(req.session, newSession(user));
            delete user.password;
            return {user};
        }else{
            return {'error': 'Account not found'}
        }
    },
    delete: async (req, res) => {
        await req.session.destroy();
        return {'success': true};
    }
});
