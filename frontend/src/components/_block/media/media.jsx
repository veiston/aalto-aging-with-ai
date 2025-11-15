import styles from "./media.module.css";

import { useMemo } from 'react';

const Media = ({ number, title, description, isReversed = false }) => {
	const formattedIndex = useMemo(() => {
		if (!number) {
			return ''
		};

		const num = Number(number);

		if (isNaN(num)) {
			return ''
		};

		return num < 10 ? '0' + num : String(num);
	}, [number]);

	return (
		<div className={`${styles["media"]} ${isReversed && styles["media--reversed"]}`}>
			<div className={styles["media__container"]}>
				{(formattedIndex || title || description) &&
					<div className={styles["media__content"]}>
						{formattedIndex &&
							<p className={styles["media__suptitle"]}>{formattedIndex}</p>
						}
						{title &&
							<h2 className={styles["media__title"]}>{title}</h2>
						}
						{description &&
							<div className={styles["media__description"]}>
								{description.split('\n').map((line, idx) => (
									<p key={idx} className="mb-s">
										{line}
									</p>
								))}
							</div>
						}
					</div>
				}
			</div>
		</div>
	);
};

export default Media;
