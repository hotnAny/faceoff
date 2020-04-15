var FACEOFF = FACEOFF || {}

FACEOFF.MAXNUMTRIALS = 20
FACEOFF.count = 0
FACEOFF.nearmisses = ['eat', 'drink', 'adjust glasses', 'listen to phone', 'raise hands']
FACEOFF.trial = []

$(document).ready(function () {
    YAML.load('user.yml', function (result) {
        FACEOFF.parts = result.parts
        // console.log(FACEOFF.parts)
    })

    document.addEventListener('keypress', function (e) {
        if (Math.random() > 0.5) {
            var idx = FACEOFF.idxTouch
            while (idx == FACEOFF.idxTouch) {
                idx = Math.floor(Math.random() * FACEOFF.parts.length)
            }
            $('#divTouch').html(FACEOFF.parts[idx])
            FACEOFF.trial.push(FACEOFF.parts[idx])
            $('#divTouch').css('opacity', '1.0')
            FACEOFF.idxTouch = idx
            $('#divNearMiss').css('opacity', '0.25')
        } else {
            var idx = FACEOFF.idxNearMiss
            while (idx == FACEOFF.idxNearMiss) {
                idx = Math.floor(Math.random() * FACEOFF.parts.length)
            }
            $('#divNearMiss').html(FACEOFF.nearmisses[idx])
            FACEOFF.trial.push(FACEOFF.nearmisses[idx])
            $('#divNearMiss').css('opacity', '1.0')
            FACEOFF.idxNearMiss = idx
            $('#divTouch').css('opacity', '0.25')
        }

        $('h1').html('Total count: ' + ++FACEOFF.count)

        if(FACEOFF.trial.length > FACEOFF.MAXNUMTRIALS) {
            alert(FACEOFF.trial)
        }

    })
})

