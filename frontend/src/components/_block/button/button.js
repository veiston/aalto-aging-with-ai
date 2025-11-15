import styles from "./button.module.css";

const Button = ({ size = "", type = "", effect = "", children, onClick }) => {
	const className = [
		styles.button,
		size && styles[`button--${size}`],
		type && styles[`button--${type}`],
		effect && styles[`button--${effect}`],
	].filter(Boolean).join(" ");

	return (
        <button className={className} onClick={onClick}>
            {children}
        </button>
    );
};

export default Button;
