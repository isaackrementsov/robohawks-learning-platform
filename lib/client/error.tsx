export function FormError(props){
    return (
        <>
            {props.error &&
                <div className="label error-label">
                    {props.error}
                </div>
            }
        </>
    );
}
