# EMS1-5105 navsideIconIts

## Purpose

Verify that the Map navigation-side icon and its position change correctly when the navigation panel is expanded and collapsed.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, and password
- DUT selected by the test execution node

## Preconditions

- EMS Web is reachable.
- The test account can open the Map page.

## Steps

1. Login to EMS Web.
2. Open `Map`.
3. Click the element whose ID is `navside_icon`.
4. Verify its `style` attribute uses `resources/images/i_action_left_arrow.png` and `margin-left: 18.7%;`.
5. Click `navside_icon` again.
6. Verify its `style` attribute uses `resources/images/i_action_right_arrow.png` and `margin-left: calc(0px);`.

## Expected Result

- The first click displays the left-arrow image at `18.7%`.
- The second click displays the right-arrow image at `calc(0px)`.

## Automation Notes

- The raw DOM `style` attribute is checked rather than computed CSS values.
- This case is marked `@pytest.mark.Unicase`.
