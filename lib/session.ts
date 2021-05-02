import { applySession } from 'next-session';
import redis from 'redis';
import connectRedis from 'connect-redis';
import session from 'express-session';

const RedisStore = require('connect-redis')(session);
const client = redis.createClient({
    host: 'localhost',
    port: 6379
});

const options = {
    store: new RedisStore({client})
}

export const useSession = async (req, res) => await applySession(req, res, options);
export const newSession = (user) : Object => {return {
    'user_id': user.id,
    'instructor': user.instructor,
}}
