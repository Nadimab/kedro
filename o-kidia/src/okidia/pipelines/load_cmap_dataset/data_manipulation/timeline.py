from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pygame
from pygame import K_SPACE, KEYUP, QUIT

from .game_session.challenge import (
    CrocosMazeChallenge,
)
from .game_session.enums import (
    ActivityEnum,
    PhaseEnum,
)
from .game_session.game_session import (
    GameSession,
)


def load_png(name):
    """Load image and return image object"""
    fullname = os.path.join("static", "img", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit(message)
    return image, image.get_rect()


class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = load_png("cursor.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = (0, 0)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect = self.rect.move(self.move)
        if self.rect.left < self.area.left:
            self.rect.left = self.area.left
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
        if self.rect.top < self.area.top:
            self.rect.top = self.area.top
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom
        pygame.event.pump()

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y


class Background:
    def __init__(self, screen: pygame.Surface) -> None:
        default_background = pygame.Surface(screen.get_size())
        default_background = default_background.convert()
        default_background.fill((0, 0, 0))
        self.__backgrounds = {
            "default": default_background,
            ActivityEnum.SCREEN_CALIBRATION.value: pygame.transform.scale(
                load_png(f"{ActivityEnum.SCREEN_CALIBRATION.value}.png")[0],
                screen.get_size(),
            ),
            ActivityEnum.MAIN_MENU.value: pygame.transform.scale(
                load_png(f"{ActivityEnum.MAIN_MENU.value}.jpg")[0],
                screen.get_size(),
            ),
        }
        activities = set(ActivityEnum) - {
            ActivityEnum.SCREEN_CALIBRATION,
            ActivityEnum.MAIN_MENU,
        }
        for activity in activities:
            phases = set(PhaseEnum)
            for phase in phases:
                self.__backgrounds[
                    f"{activity.value}_{phase.name}"
                ] = pygame.transform.scale(
                    load_png(f"{activity.value}_{phase.name}.jpg")[0],
                    screen.get_size(),
                )

    def get_background(
        self,
        activity_name: str | None = None,
        # challenge_index: int = 0,
        phase: int | None = None,
    ) -> pygame.Surface:
        """Get the game background for the given activity and challenge"""
        activity_enum = (
            ActivityEnum(activity_name) if not pd.isna(activity_name) else None
        )
        phase_enum = PhaseEnum(phase) if not pd.isna(phase) else None
        if (
            activity_enum is ActivityEnum.MAIN_MENU
            or activity_enum is ActivityEnum.SCREEN_CALIBRATION
        ):
            return self.__backgrounds[f"{activity_enum.value}"]
        elif phase_enum is not None:
            return self.__backgrounds[f"{activity_enum.value}_{phase_enum.name}"]
        return self.__backgrounds["default"]

    def draw(
        self,
        screen: pygame.Surface,
        game_session: GameSession,
        activity_name: str | None = None,
        challenge_index: int = 0,
        phase: int | None = None,
    ) -> None:
        """Draw the background for the given activity and challenge"""
        screen.blit(
            self.get_background(activity_name, challenge_index, phase=phase),
            (0, 0),
        )
        activity_enum = (
            ActivityEnum(activity_name) if not pd.isna(activity_name) else None
        )
        current_activity = game_session.get_activity(activity_enum)
        if current_activity is not None:
            current_challenge = (
                current_activity.challenges[int(challenge_index)]
                if not pd.isna(challenge_index)
                else None
            )
            if isinstance(current_challenge, CrocosMazeChallenge):
                last_point: tuple[float, float] | None = None
                for point in current_challenge.curve_points():
                    if last_point is not None:
                        pygame.draw.line(
                            screen,
                            (0, 0, 255),
                            (
                                last_point[0] * screen.get_width(),
                                (1 - last_point[1]) * screen.get_height(),
                            ),
                            (
                                point[0] * screen.get_width(),
                                (1 - point[1]) * screen.get_height(),
                            ),
                            10,
                        )
                        pygame.draw.circle(
                            screen,
                            (0, 0, 255),
                            (
                                last_point[0] * screen.get_width(),
                                (1 - last_point[1]) * screen.get_height(),
                            ),
                            5,
                        )
                        pygame.draw.circle(
                            screen,
                            (0, 0, 255),
                            (
                                point[0] * screen.get_width(),
                                (1 - point[1]) * screen.get_height(),
                            ),
                            5,
                        )
                    last_point = (point[0], point[1])


def main(json_file: Path, from_time: int = 0) -> None:
    game_session = GameSession.from_json(json_file)
    digit_inputs = game_session.to_dataframe().sort_values(by=["ts"], ascending=True)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Timeline")
    clock = pygame.time.Clock()
    current_time = from_time
    background_manager = Background(screen)

    if digit_inputs is None:
        raise ValueError("No digit inputs found in screen calibration")

    start_time = digit_inputs.iloc[0]["ts"]
    index_digit_inputs = digit_inputs[
        digit_inputs["ts"] >= start_time + from_time
    ].index[0]
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    cursor = Cursor(
        digit_inputs.iloc[index_digit_inputs]["x"] * screen_width,
        digit_inputs.iloc[index_digit_inputs]["y"] * screen_height,
    )
    cursor_sprites = pygame.sprite.RenderPlain(cursor)

    background_manager.draw(screen, game_session)
    pygame.display.flip()
    should_play = True

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    should_play = not should_play
        if not should_play:
            continue
        current_time += clock.get_time() / 1000
        if (
            index_digit_inputs + 1 < len(digit_inputs)
            and (digit_inputs.iloc[index_digit_inputs + 1]["ts"] - start_time)
            <= current_time
        ):
            index_digit_inputs += 1

        if digit_inputs.iloc[index_digit_inputs]["ts"] - start_time <= current_time:
            cursor.set_position(
                digit_inputs.iloc[index_digit_inputs]["x"] * screen_width,
                (1 - digit_inputs.iloc[index_digit_inputs]["y"]) * screen_height,
            )
        background_manager.draw(
            screen,
            game_session,
            digit_inputs.iloc[index_digit_inputs]["activity"],
            digit_inputs.iloc[index_digit_inputs]["challenge"],
            digit_inputs.iloc[index_digit_inputs]["phase"],
        )
        log_text(
            screen,
            current_time,
            digit_inputs.iloc[index_digit_inputs]["ts"],
            digit_inputs.iloc[index_digit_inputs]["activity"],
            digit_inputs.iloc[index_digit_inputs]["challenge"],
            digit_inputs.iloc[index_digit_inputs]["phase"],
            clock.get_fps(),
        )
        # screen.blit(background, cursor.rect, cursor.rect)
        cursor_sprites.update()
        if digit_inputs.iloc[index_digit_inputs]["phase_digit"] != "Ended":
            cursor_sprites.draw(screen)
        pygame.display.flip()


def log_text(
    screen,
    current_time,
    last_ts,
    activity: str,
    challenge: int,
    phase: str,
    fps,
    font_size=20,
):
    # Display some text
    font = pygame.font.Font(None, font_size)
    texts = [
        font.render(f"Current Time: {int(current_time)}", 1, (255, 255, 255)),
        font.render(f"Last TS: {int(last_ts)}", 1, (255, 255, 255)),
        font.render(f"Activity: {activity}", 1, (255, 255, 255)),
        font.render(f"Challenge: {challenge}", 1, (255, 255, 255)),
        font.render(f"Phase: {phase}", 1, (255, 255, 255)),
        font.render(f"FPS: {int(fps)}", 1, (255, 255, 255)),
    ]
    for i, text in enumerate(texts):
        screen.blit(text, (10, font_size * i))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("Crocos Timeline")
    parser.add_argument("json_file", type=Path, help="Path to the json file")
    parser.add_argument(
        "--from-time", "-t", type=int, help="Time to start from", default=0
    )
    args = parser.parse_args()
    main(**vars(args))
