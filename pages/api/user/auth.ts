import RESTController, { Authorization } from '../../../lib/controller';
import { newSession } from '../../../lib/session';
import client from '../../../lib/db';

export default RESTController(Authorization.NONE, {
    post: async (req, res) => {
        const identifier = req.body.identifier
        const password = req.body.password;

        const user = await client.user.findUnique({
            where: {
                OR: [
                    {email: identifier},
                    {username: identifier}
                ],
                AND: [
                    {password: password}
                ]
            }
        });

        Object.assign(req.session, newSession(user));
        delete user.password;

        return user;
    },
    delete: async (req, res) => {
        await req.session.destroy();
        return {data: {success: true}};
    }
});
