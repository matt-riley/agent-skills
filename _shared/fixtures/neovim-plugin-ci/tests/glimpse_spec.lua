local glimpse = require("glimpse")

describe("glimpse", function()
  it("prefixes the preview", function()
    assert.equals("glimpse: init.lua", glimpse.preview("init.lua"))
  end)
end)
