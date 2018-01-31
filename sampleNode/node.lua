gl.setup(1024 ,768)

local font = resource.load_font('vibes.ttf')

function node.render()
    font:write(120,320, "foobar", 100,1,1,1,1)
end


