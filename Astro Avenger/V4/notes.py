   # Check for collisions between bullets and stars
    collisions = pygame.sprite.groupcollide(bullet_group, star_group, True, True)
    # Check for collisions between player and stars
    collisions2 = pygame.sprite.groupcollide(spaceship_group, star_group, True, False)
   
    for collision in collisions:
        boopsound.set_volume(0.05)
        boopsound.play()
        pass

    for collision2 in collisions2:
        boopsound.set_volume(0.05)
        boopsound.play()
        hit = True
        pass

    if hit:
        lost_text = FONT.render("You Lost!", 1, "white")
        screen.blit(lost_text, (screen_width/2 - lost_text.get_width()/2, screen_height/2 - lost_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)
        break