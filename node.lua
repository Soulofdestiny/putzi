gl.setup(1920 ,1080)

local font = resource.load_font('vibes.ttf')
local logo = resource.load_image("img/logo.jpg")

function node.render()
    font:write(120,320, "foobar", 100,1,1,1,1)
    gl.clear(1,1,1,1)
    util.draw_correct(logo,0, 0, WIDTH, HEIGHT)
end


