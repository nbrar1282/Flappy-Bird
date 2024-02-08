import pygame

from components import EditableGroup, TextBox


def main():
    pygame.init()
    pygame.key.set_repeat(500, 50)
    window = pygame.display.set_mode((800, 600))

    group = EditableGroup()
    box1 = TextBox((200, 100), "Box 1", id="box1", color=(255, 255, 255), bgcolor=(0, 0, 255))
    box1.rect.topleft = (100, 100)
    group.add(box1)
    box2 = TextBox((300, 100), "Box 2", id="box2", bgcolor=(0, 255, 0))
    box2.rect.topleft = (100, 300)
    group.add(box2)
    box3 = TextBox((200, 100), "Box 3", id="box3", bgcolor=(200, 200, 200))
    box3.rect.topleft = (500, 200)
    group.add(box3)

    button = TextBox((120, 100), "Save", id="save_button", bgcolor=(0, 200, 0), font_size=48)
    button.rect.topleft = (300, 450)

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)
        window.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if button.rect.collidepoint(event.pos):
                    data = {s.id: s.text for s in group.sprites()}
                    print(data)
                group.manage_click(event)
            if event.type == pygame.KEYDOWN:
                group.manage_key(event)

        group.draw(window)
        window.blit(button.image, button.rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
