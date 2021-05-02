import { Authorization } from '../../../lib/common-types';
import RESTController from '../../../lib/controller';
import { newSession } from '../../../lib/session';
import client from '../../../lib/db';

export default RESTController(Authorization.GUEST, {
    post: async (req, res) => {
        try {
            let user = await client.user.create({data: {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                username: req.body.username,
                password: req.body.password,
                email: req.body.email,
                instructor: req.body.instructor
            }});

            Object.assign(req.session, newSession(user));
            delete user.password;
            return {user};
        }catch(e){
            const field = e.meta.target.split('_')[0];
            const title = field[0].toUpperCase() + field.slice(1, field.length).toLowerCase();

            return {'error': title + ' "' + req.body[field] + '" is taken'}
        }
    }
});
