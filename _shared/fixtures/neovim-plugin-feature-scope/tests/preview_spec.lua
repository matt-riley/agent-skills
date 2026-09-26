local preview = require("glimpse.preview")

describe("preview", function()
  it("truncates long paths", function()
    assert.equals("abc…", preview.render("abcdef", 4))
  end)
end)
