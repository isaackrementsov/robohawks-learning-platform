import RESTController, { Authorization } from '../../../lib/controller';
import client from '../../../lib/db';

export default RESTController(Authorization.USER, {
    get: (_req, res) => {
        return {};
    },
    post: (_req, res) => {
        return {};
    },
    patch: (_req, res) => {
        return {};
    },
    delete: (_req, res) => {
        return {};
    }
});
