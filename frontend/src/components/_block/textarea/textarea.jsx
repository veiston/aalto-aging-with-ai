import styles from './textarea.module.scss';

const Textarea = ({ placeholder = '', required = false, rows = 4 }) => {
	return (
		<textarea
			className={styles.textarea}
			placeholder={placeholder}
			required={required}
			rows={rows}
		/>
	);
};

export default Textarea;