import styles from "./plate-wide.module.scss";

const PlateWide = ({ image, title, description, startDate, endDate }) => {
	const period = startDate || endDate ? startDate + " – " + endDate : null;

	return (
		<div className={styles["plate-wide"]}>
			<div className={styles["plate-wide__header"]}>
				<div className={styles["plate-wide__media"]}>
                    {image &&
                        <img
                            className={styles["plate-wide__image"]}
                            src={image}
                            alt={title}
                        />
                    }
                    {title &&
                        <p className={styles["plate-wide__title"]}>
                            {title}
                        </p>
                    }
				</div>
				{period &&
					<div className={styles["plate-wide__caption"]}>
                        {period}
                    </div>
                }
			</div>
            {description &&
                <p className={styles["plate-wide__content"]}>
                    {description.split('\n').map((line, idx) => (
                        <span key={idx}>
                            {line}
                            <br />
                        </span>
                    ))}
                </p>
            }
		</div>
	);
};

export default PlateWide;
