gl.setup(1920 ,1080)

local font = resource.load_font('vibes.ttf')
local logo = resource.load_image("logo.jpg")

function node.render()
    gl.clear(0,0,0,0)
    font:write(120,320, "foobar", 100,1,1,1,1)
    util.draw_correct(logo,WIDTH*0.6, HEIGHT*0.6, WIDTH, HEIGHT)
end


