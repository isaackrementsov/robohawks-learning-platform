import Nav from '../lib/client/nav';

export default function Index(){
    return (
        <div className="App gradient-app">
            <Nav logo={'logo-white'}/>
            <div className="jumbotron jumbotron-fluid gradient flex-container-center">
                <div className="row center">
                    <div className="col-md-6">
                        <h1>Microcredentials, managed</h1>
                        <p>
                            LearnCVU is a platform for skills-based learning and educational content management.
                            Our versatile course-design interface and seamless integration of microcredentials makes online teaching a breeze.
                        </p>
                    </div>
                    <div className="col-md-6">
                        <img src="/img/landing.png" alt="Landing" id="landing"/>
                    </div>
                </div>
            </div>
        </div>
    );
}
