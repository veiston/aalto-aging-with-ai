import styles from './input.module.css';

const Input = ({ type = 'text', placeholder = '', required = false }) => {
	return (
		<input
			className={styles.input}
			type={type}
			placeholder={placeholder}
			required={required}
		/>
	);
};

export default Input;