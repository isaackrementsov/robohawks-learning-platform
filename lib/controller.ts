import { NextApiRequest, NextApiResponse } from 'next';
import globalMiddleware from './middleware';

export enum Authorization {
    NONE,
    GUEST,
    USER,
    INSTRUCTOR
}

const baseResolvers = {
    'GET': (_req, _res) => { return {}; }
}

const authorized = (authorization, session) : Boolean => {
    switch(authorization){
        case Authorization.GUEST:
            return !session.userId;

        case Authorization.USER:
            return !!session.userId;

        case Authorization.INSTRUCTOR:
            return !!session.userId && session.instructor;

        default:
            return true;
    }
}

export default function RESTController(authorization: Authorization = Authorization.NONE, resolvers: Object = baseResolvers, controllerMiddleware: Function[] = []) : Function {

    const handler = async (req: NextApiRequest, res: NextApiResponse) => {
        try {
            for(let i = 0; i < globalMiddleware.length; i++) await globalMiddleware[i](req, res);
            for(let i = 0; i < controllerMiddleware.length; i++) await controllerMiddleware[i](req, res);

            if(authorized(authorization, req['session'])){
                const resolve = resolvers[req.method.toLowerCase()];

                if(resolve){
                    const data = await resolve(req, res);
                    res.status(200).json(data);
                }else{
                    res.status(501).json({error: 'Method ' + req.method + ' not supported for endpoint ' + req.url})
                }
            }else{
                res.status(403).json({error: 'You are not authorized to access endpoint ' + req.url})
            }
        }catch(e){
            res.status(500).json({error: 'Server error'});
        }
    }

    return handler;
}
