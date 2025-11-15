import styles from "./card.module.css";

const Card = ({ image, description, title, subtitle }) => {
	return (
		<div className={styles["card"]}>
			<div className={styles["card__container"]}>
				<div className={styles["card__picture"]}>
					<img className={styles["card__image"]} src={image} alt={title} />
				</div>
				<p className={styles["card__description"]}>{description}</p>
				<div className={styles["card__divider"]}></div>
				<h3 className={styles["card__title"]}>{title}</h3>
				<p className={styles["card__subtitle"]}>{subtitle}</p>
			</div>
		</div>
	);
};

export default Card;