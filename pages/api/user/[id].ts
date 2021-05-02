import { Authorization } from '../../../lib/common-types';
import RESTController from '../../../lib/controller';
import client from '../../../lib/db';

export default RESTController(Authorization.USER, {
    get: async (req, res) => {
        let { id } = req.query;
        id = parseInt(id);

        const user = await client.user.findUnique({where: {id: id}});

        return {user};
    },
    patch: (_req, res) => {
        return {};
    },
    delete: (_req, res) => {
        return {};
    }
});
