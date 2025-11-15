import styles from "./plate.module.css";

const Plate = ({ title, icon }) => {
	return (
		<div className={styles["plate"]}>
			{icon && (
				<div className={styles["plate__icon"]}>
					{icon}
				</div>
			)}
			{title && (
				<p className={styles["plate__title"]}>
					{title}
				</p>
			)}
		</div>
	);
};

export default Plate;